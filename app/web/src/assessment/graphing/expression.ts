/* The graphing panel's own expression language, parsed and evaluated here because the content
   security policy forbids eval and new Function, and because 05 rules out loading Desmos or any
   third-party calculator. It reads one function of x: + - * / ^, parentheses, unary minus,
   implicit multiplication (2x, 3sin(x), (x+1)(x-1)), the functions below, pi and e. */

export type AngleMode = "radians" | "degrees";

export type Expression =
   | { kind: "number"; value: number }
   | { kind: "variable" }
   | { kind: "negate"; operand: Expression }
   | { kind: "binary"; operator: "+" | "-" | "*" | "/" | "^"; left: Expression; right: Expression }
   | { kind: "call"; name: FunctionName; argument: Expression };

export type FunctionName =
   | "sin"
   | "cos"
   | "tan"
   | "sec"
   | "csc"
   | "cot"
   | "arcsin"
   | "arccos"
   | "arctan"
   | "ln"
   | "log"
   | "exp"
   | "sqrt"
   | "abs";

const FUNCTION_NAMES: FunctionName[] = [
   "arcsin",
   "arccos",
   "arctan",
   "sqrt",
   "sin",
   "cos",
   "tan",
   "sec",
   "csc",
   "cot",
   "exp",
   "abs",
   "log",
   "ln"
];

const CONSTANT_NAMES = ["pi", "e"];

const DIRECT_TRIGONOMETRY: FunctionName[] = ["sin", "cos", "tan", "sec", "csc", "cot"];

const INVERSE_TRIGONOMETRY: FunctionName[] = ["arcsin", "arccos", "arctan"];

type Token =
   | { kind: "number"; value: number }
   | { kind: "name"; name: string }
   | { kind: "operator"; symbol: string }
   | { kind: "open" }
   | { kind: "close" };

export class ExpressionError extends Error {
   constructor(message: string) {
      super(message);

      this.name = "ExpressionError";
   }
}

/* A run of letters is split into the known names greedily, longest first, so "xsin" reads as x
   times sin and "ex" as e times x. */
function namesIn(letters: string) {
   const lowered = letters.toLowerCase();
   const knownNames = [...FUNCTION_NAMES, ...CONSTANT_NAMES, "x"];
   const names: string[] = [];
   let index = 0;

   while (index < lowered.length) {
      const match = knownNames.find((name) => lowered.startsWith(name, index));

      if (match === undefined) {
         throw new ExpressionError(`"${letters}" is not a name this panel knows.`);
      }

      names.push(match);
      index += match.length;
   }

   return names;
}

export function tokenize(source: string): Token[] {
   const tokens: Token[] = [];
   const text = source.replace(/π/g, "pi").replace(/·|×/g, "*").replace(/−/g, "-");
   let index = 0;

   while (index < text.length) {
      const character = text[index];
      const isSpace = /\s/.test(character);
      const startsNumber = /[0-9.]/.test(character);
      const startsName = /[A-Za-z]/.test(character);

      if (isSpace) {
         index += 1;
         continue;
      }

      if (startsNumber) {
         const match = /^(\d+\.?\d*|\.\d+)/.exec(text.slice(index));

         if (match === null) {
            throw new ExpressionError("A number is written wrongly.");
         }

         tokens.push({ kind: "number", value: Number(match[1]) });
         index += match[1].length;
         continue;
      }

      if (startsName) {
         const letters = /^[A-Za-z]+/.exec(text.slice(index))![0];

         for (const name of namesIn(letters)) {
            tokens.push({ kind: "name", name });
         }

         index += letters.length;
         continue;
      }

      if ("+-*/^".includes(character)) {
         tokens.push({ kind: "operator", symbol: character });
         index += 1;
         continue;
      }

      if (character === "(") {
         tokens.push({ kind: "open" });
         index += 1;
         continue;
      }

      if (character === ")") {
         tokens.push({ kind: "close" });
         index += 1;
         continue;
      }

      throw new ExpressionError(`"${character}" is not a symbol this panel reads.`);
   }

   return tokens;
}

class Parser {
   private position = 0;

   constructor(private readonly tokens: Token[]) {}

   parse(): Expression {
      const isEmpty = this.tokens.length === 0;

      if (isEmpty) {
         throw new ExpressionError("Type a function of x.");
      }

      const expression = this.sum();
      const hasLeftover = this.position < this.tokens.length;

      if (hasLeftover) {
         throw new ExpressionError("Part of the expression could not be read.");
      }

      return expression;
   }

   private peek(): Token | undefined {
      return this.tokens[this.position];
   }

   private isOperator(symbol: string) {
      const token = this.peek();

      return token !== undefined && token.kind === "operator" && token.symbol === symbol;
   }

   private startsOperand() {
      const token = this.peek();

      if (token === undefined) {
         return false;
      }

      return token.kind === "number" || token.kind === "name" || token.kind === "open";
   }

   private sum(): Expression {
      let expression = this.product();

      while (this.isOperator("+") || this.isOperator("-")) {
         const operator = (this.tokens[this.position] as { symbol: "+" | "-" }).symbol;

         this.position += 1;
         expression = { kind: "binary", operator, left: expression, right: this.product() };
      }

      return expression;
   }

   private product(): Expression {
      let expression = this.signed();

      while (true) {
         const isExplicit = this.isOperator("*") || this.isOperator("/");

         if (isExplicit) {
            const operator = (this.tokens[this.position] as { symbol: "*" | "/" }).symbol;

            this.position += 1;
            expression = { kind: "binary", operator, left: expression, right: this.signed() };
            continue;
         }

         if (this.startsOperand()) {
            expression = { kind: "binary", operator: "*", left: expression, right: this.power() };
            continue;
         }

         return expression;
      }
   }

   private signed(): Expression {
      if (this.isOperator("-")) {
         this.position += 1;

         return { kind: "negate", operand: this.signed() };
      }

      if (this.isOperator("+")) {
         this.position += 1;

         return this.signed();
      }

      return this.power();
   }

   private power(): Expression {
      const base = this.primary();

      if (this.isOperator("^")) {
         this.position += 1;

         return { kind: "binary", operator: "^", left: base, right: this.signed() };
      }

      return base;
   }

   private primary(): Expression {
      const token = this.peek();

      if (token === undefined) {
         throw new ExpressionError("The expression ends too early.");
      }

      this.position += 1;

      if (token.kind === "number") {
         return { kind: "number", value: token.value };
      }

      if (token.kind === "open") {
         const inner = this.sum();
         const closing = this.peek();
         const isClosed = closing !== undefined && closing.kind === "close";

         if (!isClosed) {
            throw new ExpressionError("A bracket is not closed.");
         }

         this.position += 1;

         return inner;
      }

      if (token.kind === "name") {
         return this.named(token.name);
      }

      throw new ExpressionError("The expression has a symbol out of place.");
   }

   private named(name: string): Expression {
      if (name === "x") {
         return { kind: "variable" };
      }

      if (name === "pi") {
         return { kind: "number", value: Math.PI };
      }

      if (name === "e") {
         return { kind: "number", value: Math.E };
      }

      const opening = this.peek();
      const hasBracket = opening !== undefined && opening.kind === "open";

      if (!hasBracket) {
         throw new ExpressionError(`Write ${name} with brackets, as in ${name}(x).`);
      }

      return { kind: "call", name: name as FunctionName, argument: this.primary() };
   }
}

export function parseExpression(source: string): Expression {
   return new Parser(tokenize(source)).parse();
}

function applyFunction(name: FunctionName, argument: number, mode: AngleMode) {
   const isDirectTrig = DIRECT_TRIGONOMETRY.includes(name);
   const isInverseTrig = INVERSE_TRIGONOMETRY.includes(name);
   const isDegrees = mode === "degrees";
   const angle = isDirectTrig && isDegrees ? (argument * Math.PI) / 180 : argument;
   let value: number;

   switch (name) {
      case "sin":
         value = Math.sin(angle);
         break;
      case "cos":
         value = Math.cos(angle);
         break;
      case "tan":
         value = Math.tan(angle);
         break;
      case "sec":
         value = 1 / Math.cos(angle);
         break;
      case "csc":
         value = 1 / Math.sin(angle);
         break;
      case "cot":
         value = 1 / Math.tan(angle);
         break;
      case "arcsin":
         value = Math.asin(argument);
         break;
      case "arccos":
         value = Math.acos(argument);
         break;
      case "arctan":
         value = Math.atan(argument);
         break;
      case "ln":
         value = Math.log(argument);
         break;
      case "log":
         value = Math.log10(argument);
         break;
      case "exp":
         value = Math.exp(argument);
         break;
      case "sqrt":
         value = Math.sqrt(argument);
         break;
      case "abs":
         value = Math.abs(argument);
         break;
   }

   const convertsBack = isInverseTrig && isDegrees;

   return convertsBack ? (value * 180) / Math.PI : value;
}

export function evaluate(expression: Expression, x: number, mode: AngleMode): number {
   switch (expression.kind) {
      case "number":
         return expression.value;
      case "variable":
         return x;
      case "negate":
         return -evaluate(expression.operand, x, mode);
      case "call":
         return applyFunction(expression.name, evaluate(expression.argument, x, mode), mode);
      case "binary": {
         const left = evaluate(expression.left, x, mode);
         const right = evaluate(expression.right, x, mode);

         switch (expression.operator) {
            case "+":
               return left + right;
            case "-":
               return left - right;
            case "*":
               return left * right;
            case "/":
               return left / right;
            case "^":
               return Math.pow(left, right);
         }
      }
   }
}

export type RealFunction = (x: number) => number;

export function compile(source: string, mode: AngleMode): RealFunction {
   const expression = parseExpression(source);

   return (x: number) => evaluate(expression, x, mode);
}
