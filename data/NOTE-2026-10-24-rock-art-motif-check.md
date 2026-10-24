# Note: rabbit, felid and turtle motifs in the Côa rock art (2026-10-24)

**Status:** checked. The page wording is corrected in this commit. Preprint §8.1 and the abstract still need the same correction before the next Zenodo version.

## What was checked

The page and the preprint (§8.1, abstract) said that none of the three animals, the rabbit, the wildcat and the pond turtle, is known in the Côa rock art. Two sources were checked:

1. **Reis, M., "'Mil rochas e tal...!': inventário dos sítios da arte rupestre do Vale do Côa"**, *Portvgalia* 33, 34 and 35 (three parts; the OJS pages date all three 2018, the print volumes are 2012-2014). Full text, searched for *coelho, lebre, lagomorfo, gato, felino, lince, cágado, tartaruga, quelónio*.
   - Part 1: <https://ojs.letras.up.pt/index.php/Port/article/view/3619>
   - Part 2: <https://ojs.letras.up.pt/index.php/Port/article/view/3562>
   - Part 3 (conclusão): <https://ojs.letras.up.pt/index.php/Port/article/view/3555>
2. **Baptista, A.A., Miguel, I., Galvão, J. and Botica, N. (2026), "Vale do Côa rock art as linked open data"**, *Open Research Europe* 6, <https://doi.org/10.12688/openreseurope.21901.1>. Its SKOS values vocabulary (<https://doi.org/10.34622/datarepositorium/2SGCAG>) and RDF data were queried on the project's SPARQL endpoint (GraphDB, repository `RARAA`, <http://openmydata.dsi.uminho.pt:7200/repositories/RARAA>).

## What was found

**Rabbit (lagomorphs): two possible figures, Palaeolithic, plus hares in a modern-era scene.**
- Vermelhosa, rock 2: "dois animais de difícil interpretação, ambos incompletos por fracturação, e que poderiam ser representações de lagomorfos (ou seja, coelhos ou lebres). A confirmar-se, seriam as únicas conhecidas na região da arte do Côa" (Reis, part 2).
- Ribeira da Cabreira, rock 1: a modern-era (Época Moderna) hunting scene with "um canídeo de boca aberta e dentes à mostra que persegue lebres" (Reis, part 2). Hares, not rabbits, and not ancient.

**Wildcat (felids): three possible figures, Palaeolithic.**
- Ribeira de Piscos, Quinta da Barca and Broeira, "três possíveis felinos" (Reis, part 3). At Broeira, rock 4: a single-line quadruped "de difícil identificação, mas que poderá ser um felino" (Reis, part 1).
- Reis on all of these minor animals: "são sempre figuras pouco definidas nos aspectos que permitem a sua identificação como espécie, deixando-nos sempre na dúvida se a interpretação estará correcta" (part 3).
- The linked-open-data vocabulary has a `Felid` concept (also `Mustelid`, `Canid`, `Bird`, `Fish`, `Serpent`), but no motif in the published data uses it. The data covers one site only, Vale da Vermelhosa (144 motifs).

**Pond turtle: none.** No mention in any of the three Reis parts. The vocabulary has no lagomorph, turtle or chelonian concept.

**Iron Age (the reference style for the plates):** Reis describes the Iron Age engravings as horses, deer, geometric motifs, warriors and weapons. None of the possible rabbits or felids is Iron Age.

## What changes

The accurate statement is: (i) the pond turtle is not known in the Côa rock art; (ii) the rabbit and the wildcat appear at most as a handful of uncertain Palaeolithic figures (two possible lagomorphs, three possible felids), which the inventory's own author doubts; (iii) none of the three is known in the Iron Age fine-line engravings the plates take their style from.

- `index.html`: the opening sentence of "New animals in an old line" is corrected in EN/PT/ES/FR, with a short note linking here.
- Still to do: preprint §8.1 and abstract (`Solo-field-illustrator-project-for-Rewilding-Portugal/research/rewilding-dynamics/zenodo-preprint/article.md`), and the reference entry for Reis (2018), which needs the journal, volumes and the three parts.

A detail worth keeping: the two possible lagomorphs are at Vermelhosa, the same site as the Iron Age rock 3 (Botica et al., 2023) used as the drawing reference.
