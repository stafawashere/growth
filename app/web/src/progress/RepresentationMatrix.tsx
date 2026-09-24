import type { RepresentationCell, RepresentationMatrixPayload } from "../api/types";

/* 08 "Information architecture", progress: the representation matrix, source representation by
   target representation (11 P7 scope item 7). A cell exists only for a pair the BC-REP taxonomy
   lists as a conversion, so any other pair is left blank rather than drawn as a zero. An attempt
   whose archetype carries several conversion pairs counts in each of them, which is why the
   section states the attempt count beside the cells instead of leaving the cells to be summed. */

export interface RepresentationMatrixProps {
   matrix: RepresentationMatrixPayload;
}

function cellKey(source: string, target: string) {
   return `${source}>${target}`;
}

function cellText(cell: RepresentationCell) {
   const hasAttempts = cell.attempts > 0;

   if (!hasAttempts) {
      return "no attempts";
   }

   return `${cell.correct} of ${cell.attempts}`;
}

export function RepresentationMatrix({ matrix }: RepresentationMatrixProps) {
   const cells = new Map(matrix.cells.map((cell) => [cellKey(cell.source, cell.target), cell]));
   const hasPairs = matrix.representations.length > 0;

   return (
      <section aria-labelledby="representation-heading" data-testid="representation-matrix">
         <h2 id="representation-heading" className="section-heading">
            Representations, source by target
         </h2>

         <p className="caption" data-testid="translation-attempts">
            {matrix.translation_attempts} of {matrix.practice_attempts} graded practice attempts asked for a
            translation between two representations. An attempt that asked for more than one counts in each
            of their cells.
         </p>

         {hasPairs ? (
            <table>
               <caption className="caption">
                  Correct of attempted, from the row&apos;s representation to the column&apos;s. A blank cell is a
                  pair the taxonomy does not list as a translation.
               </caption>
               <thead>
                  <tr>
                     <th scope="col">From</th>
                     {matrix.representations.map((target) => (
                        <th key={target.id} scope="col">
                           {target.name}
                        </th>
                     ))}
                  </tr>
               </thead>
               <tbody>
                  {matrix.representations.map((source) => (
                     <tr key={source.id}>
                        <th scope="row">{source.name}</th>
                        {matrix.representations.map((target) => {
                           const cell = cells.get(cellKey(source.id, target.id));

                           return (
                              <td key={target.id} data-testid="representation-cell">
                                 {cell === undefined ? "" : cellText(cell)}
                              </td>
                           );
                        })}
                     </tr>
                  ))}
               </tbody>
            </table>
         ) : (
            <p className="muted">The taxonomy lists no translation between representations yet.</p>
         )}
      </section>
   );
}