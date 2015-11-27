#include <iostream>
#include <fstream>
#include <vector>
#include "CsvReader.h"


int main() {
  std::map<std::string, int> possible;
  std::map<std::string, std::map<std::string, int>> favorable;

  std::ifstream train("/home/martin/Documents/repos/datos/entrega/trainFilteredSinBinarizarV3-columnas.csv");
  CsvReader reader(train);

  RowMap row;
  while (reader.next(row)) {
    std::string row_key = row["Zipcode"] += row["Daylight"] += row["CrimeAsociationDual"];
    possible[row_key] += 1;
    favorable[row_key][row["Category"]] += 1;
  }

  for (std::map<std::string, int>::iterator it = possible.begin();
       it != possible.end(); it++) {
    std::cout << "Key: " << it->first << std::endl
              << "\tTotal: " << it->second << std::endl;
    for (std::map<std::string, int>::iterator it2 = favorable[it->first].begin();
         it2 != favorable[it->first].end(); it2++) {
      std::cout << "\t" << it2->first << ": " << it2->second << std::endl;
    }

    std::cout << std::endl;
  }

  return 0;
}
