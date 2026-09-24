/* A measured figure is printed to two decimal places at most, and a whole number as it is. */
export function formatFigure(value: number) {
   return String(Number(value.toFixed(2)));
}