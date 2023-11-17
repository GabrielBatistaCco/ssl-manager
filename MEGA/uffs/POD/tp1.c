#include <stdio.h>
#include <stdlib.h>
#include <time.h>
// Reaproveitar?
int *gerarListaAleatoria(int tamanho, int inicioIntervalo, int fimIntervalo) {
    int *lista = (int *)malloc(tamanho * sizeof(int));
    srand(time(NULL));
    for (int i = 0; i < tamanho; i++) {
        lista[i] = rand() % (fimIntervalo - inicioIntervalo + 1) + inicioIntervalo;
    }
    return lista;
}

void printarLista(int lista[], int tamanho) {
    for (int i = 0; i < tamanho; i++) {
        printf("%d ", lista[i]);
    }
    printf("\n");
}

void troca(int *valor1, int *valor2){
    int temp = *valor1;
    *valor1 = *valor2;
    *valor2 = temp;
}

void media(int lista[], int tamanho){
    clock_t inicio = clock();
    bubbleSort(lista, tamanho);
    clock_t fim = clock();

    clock_t inicio2 = clock();
    bubbleSort(lista, tamanho);
    clock_t fim2 = clock();

    clock_t inicio3 = clock();
    bubbleSort(lista, tamanho);
    clock_t fim3 = clock();

    double bubbleSortmedia = ((((double)(inicio - fim)) / CLOCKS_PER_SEC) + (((double)(inicio2 - fim2)) / CLOCKS_PER_SEC) + (((double)(inicio3 - fim3)) / CLOCKS_PER_SEC))/3;
    printf("%f \n", bubbleSortmedia);
}

//

void bubbleSort(int lista[], int tamanho) {
    for (int i = tamanho -1; i >= 1; i--) {
        for (int j = 0; j < i; j++){
            if (lista[j] > lista[j + 1]){
                troca(&lista[j], &lista[j + 1]);
            }
        }
    }
}

int main() {
    int tamanho1 = 1000;
    int tamanho2 = 5000;
    int tamanho3 = 10000;
    int tamanho4 = 50000;
    int tamanho5 = 100000;
    int tamanho6 = 1000000;
    int *lista1 = gerarListaAleatoria(tamanho1, 0, tamanho1);
    int *lista2 = gerarListaAleatoria(tamanho2, 0, tamanho2);
    int *lista3 = gerarListaAleatoria(tamanho3, 0, tamanho3);
    int *lista4 = gerarListaAleatoria(tamanho4, 0, tamanho4);
    int *lista5 = gerarListaAleatoria(tamanho5, 0, tamanho5);
    int *lista6 = gerarListaAleatoria(tamanho6, 0, tamanho6);

    media(lista1, tamanho1);

    free(lista1);
    free(lista2);
    free(lista3);
    free(lista4);
    free(lista5);
    free(lista6);
    return 0;
}