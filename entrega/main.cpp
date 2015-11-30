#include <fstream>
#include <iostream>
#include "Predictor.h"


int main(int argc, char *argv[]) {
  std::ifstream train(argc == 3 ? argv[1] :
                                  "/home/martin/Documents/repos/datos/entrega/trainFilteredSinBinarizarV3-columnas.csv");
  std::ifstream test(argc == 3 ? argv[2] :
                                 "/home/martin/Documents/repos/datos/entrega/testFilteredSinBinarizarV3-columnas.csv");

  Predictor predictor;
  predictor.train(train);
  predictor.predict(test, std::cout);

  return 0;
}
