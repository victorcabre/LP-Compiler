### Víctor Cabré Guerrero
# Pràctica LP 2023-2024 Q1: PandaQ

PandaQ és un intèrpret de SQL basat en Pandas. L'intèrpret ofereix una interfície web senzilla, a través de la qual es poden fer consultes i visualitzar els resultats.


## Com executar PandaQ?
1. Per executar, has de tenir instal·lat Streamlit, Pandas i ANTLR4. Pots fer-ho utilitzant les següents comandes:
`pip install streamlit`, `pip install pandas`, `pip install antlr4-tool`, `pip install antlr4-python3-runtime`

2. Assegurat que hagis descomprimit `pandaQ.py` i `pandaQ.g4` al mateix directori.

3. A continuació, genera el Parser i el Lexer a partir del fitxer `pandaQ.g4`. Pots fer-ho amb la següent comanda:
`antlr4 -Dlanguage=Python3 -no-listener -visitor pandaQ.g4`

4. Crea una carpeta dins del directori i anomena-la `data`. Ho pots fer amb `mkdir data`.

5. Posa els fitxers CSV dins de la carpeta `data`

6. Executa el programa amb Streamlit: `streamlit run pandaQ.py`


## Com utilitzo el programa?

La interfície gràfica té un element principal, una caixa de text on pots escriure les teves _queries_. Pots encadenar diversos _statements_ dins de la mateixa _query_.

Per exemple, pots fer:

    select * from countries;

També:

    q := select first_name, last_name, job_title, department_name from employees inner join departments on department_id=department_id inner join jobs on job_id=job_id;

    select first_name, last_name from q;

Per enviar la consulta, fes clic a qualsevol zona fora de la caixa de text o prem Ctrl+Enter. El resultat apareixerà just a sota de la caixa de text. Si hi ha més d'un resultat, apareixeran ordenats cronològicament.