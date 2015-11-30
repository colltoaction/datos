#include <fstream>
#include <iostream>
#include "Predictor.h"


int main(int argc, char *argv[]) {
  std::ifstream train(argv[1]);
  std::ifstream test(argv[2]);

  Predictor predictor;
  predictor.train(train);
  predictor.predict(test, std::cout);

  return 0;
}
