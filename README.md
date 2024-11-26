# UFSC-INE5421-EI5
Nesta atividade, você deverá implementar um programa em Python para construir a tabela de análise de um Analisador Sintático do tipo Preditivo LL(1). Para isso você vai precisar calcular os conjuntos First e Follow da Gramática de Entradas. Reutilize o código do EI4. Assume-se que a gramática esteja fatorada e não seja recursiva à esquerda. Contudo, certifique-se de que ela é LL(1).

Formato de Entrada

{NT}{T}{NT Inicial}{Produções};"sentença_de_entrada"

Onde:

    {NT} é a lista de não-terminais.
    {T} é a lista de terminais.
    {NT Inicial} é o símbolo inicial da gramática.
    {Produções} é a lista de produções separadas por ';'.

Cada produção tem o formato:

"<Não-terminal> = <Corpo da produção>"

Onde <Corpo da produção> pode ser uma sequência de símbolos terminais e não-terminais, e pode também conter o símbolo & que representa a produção vazia (epsilon). Atenção ao fato de que & não é um Terminal, logo não aparece na definição de G.

Formato de Saída

A saída do programa deve ser uma string no seguinte formato:

<<Tabela de análise><sim/não>>

Onde a Tabela de análise tem o seguinte formato:

<{NT};Simbolo_inicial;{alfabeto};[linha,coluna, produção]>
Exemplo de Entrada e Saída
Entrada:

{E,A,T,B,F}{m,v,i,o,c}{E}{E = TA; A = mTA; A = &; T = FB; B = vFB; B = &; F = i; F = oEc};"oimicvi"



"{P, K,V,C}{c,v,f,i,b,e,m}{P}{P = KVC; K = cK; K = &; V = vV; V = F; F = fPiF; F = &; C = bVCe; C = miC; C = &;}"
Saída:

<<{A,B,E,F,T};E;{c,i,m,o,v,$};[A,c,&][A,m,mTA][A,$,&][B,c,&][B,m,&][B,v,vFB][B,$,&][E,i,TA][E,o,TA][F,i,i][F,o,oEc][T,i,FB][T,o,FB]><sim>>

Instruções

    Arquivo Principal: Todo o código deve estar presente no arquivo main.py, que será fornecido a você. Certifique-se de que todas as funções e lógica necessárias estejam contidas neste arquivo.
    Formato da Saída: Mantenha a saída no formato especificado. Cada subconjunto está ordenado em ordem lexicográfica crescente.

Observações

    Tratamento de Vazio: Utilize o símbolo & para representar a produção vazia (epsilon).
