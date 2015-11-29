#include <fstream>
#include <iostream>
#include "Predictor.h"


int main(int argc, char *argv[]) {
  std::cout << std::endl <<
     "   dP                 oo          oo   dP                           dP                      " << std::endl <<
     "   88                                  88                           88                      " << std::endl <<
     "   88        dP    dP dP .d8888b. dP d8888P .d8888b.    dP    dP    88 .d8888b. .d8888b.    " << std::endl <<
     "   88        88    88 88 Y8ooooo. 88   88   88'  `88    88    88    88 88'  `88 Y8ooooo.    " << std::endl <<
     "   88        88.  .88 88       88 88   88   88.  .88    88.  .88    88 88.  .88       88    " << std::endl <<
     "   88888888P `88888P' dP `88888P' dP   dP   `88888P'    `8888P88    dP `88888P' `88888P'    " << std::endl <<
     "                                                             .88                            " << std::endl <<
     "                                                         d8888P                             " << std::endl <<
     "                                                                                            " << std::endl <<
     "888888ba             dP                                                oo                   " << std::endl <<
     "88    `8b            88                                                                     " << std::endl <<
     "88     88 .d8888b. d8888P .d8888b. .d8888b. .d8888b. dP    dP 88d888b. dP .d8888b. .d8888b. " << std::endl <<
     "88     88 88'  `88   88   88'  `88 Y8ooooo. 88'  `88 88    88 88'  `88 88 88'  `88 Y8ooooo. " << std::endl <<
     "88    .8P 88.  .88   88   88.  .88       88 88.  .88 88.  .88 88       88 88.  .88       88 " << std::endl <<
     "8888888P  `88888P8   dP   `88888P' `88888P' `88888P8 `88888P' dP       dP `88888P' `88888P' " << std::endl <<
     "                                                                                            " << std::endl <<
     "                                                                                            " << std::endl <<
     "                            Alumno                     |  Padrón                            " << std::endl <<
     "                            ------------------------------------                            " << std::endl <<
     "                            Castro Pippo, Juan Manuel  |  93.760                            " << std::endl <<
     "                            González Coll, Martín      |  94.322                            " << std::endl <<
     "                            Ordoñez, Francisco         |  96.478                            " << std::endl <<
     "                            Sueiro, Ignacio Andrés     |  96.817                            " << std::endl;

  std::cin.get();
  std::ifstream train(argc == 3 ? argv[1] :
                                  "/home/martin/Documents/repos/datos/entrega/trainFilteredSinBinarizarV3-columnas.csv");
  std::ifstream test(argc == 3 ? argv[2] :
                                 "/home/martin/Documents/repos/datos/entrega/testFilteredSinBinarizarV3-columnas.csv");

  Predictor predictor;
  predictor.train(train);
  predictor.predict(test, std::cout);

  return 0;
}
