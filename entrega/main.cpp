#include <iostream>
#include <fstream>
#include <vector>
#include "CsvReader.h"


int main() {
  std::ifstream train("/home/martin/Documents/repos/datos/entrega/trainFilteredSinBinarizarV3.csv");
  CsvReader reader(train);

  RowMap row;
  while (reader.next(row)) {
    std::cout << "Reading Coordinate: " << row["Coordinate"] << "" << std::endl;
  }

  return 0;
}
