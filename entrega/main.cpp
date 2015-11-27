#include <fstream>
#include "Predictor.h"


int main() {
  std::ifstream train("/home/martin/Documents/repos/datos/entrega/trainFilteredSinBinarizarV3-columnas.csv");
  std::ifstream test("/home/martin/Documents/repos/datos/entrega/testFilteredSinBinarizarV3-columnas.csv");
  std::ofstream predicted("/media/martin/MARTIN/predicted.csv");

  Predictor predictor;
  predictor.train(train);
  predictor.predict(test, predicted);

  return 0;
}
