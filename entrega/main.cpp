#include <fstream>
#include <iostream>
#include "Predictor.h"


int main(int argc, char *argv[]) {
  std::ifstream train(argc == 3 ? argv[1] :
                                  "/home/martin/Documents/repos/datos/entrega/trainSuperDuperFinal2.csv");
  std::ifstream test(argc == 3 ? argv[2] :
                                 "/home/martin/Documents/repos/datos/entrega/testSuperDuperFinal2.csv");

  Predictor predictor;
  predictor.train(train);
  predictor.predict(test, std::cout);

  return 0;
}
