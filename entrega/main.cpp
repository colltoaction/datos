#include <iostream>
#include <fstream>
#include <vector>
#include "CsvReader.h"


std::string get_row_key(RowMap &row) {
  return row["Zipcode"] += row["Daylight"] += row["CrimeAsociationDual"];
}

void train(std::map<std::string, int> &possible,
           std::map<std::string, std::map<std::string, int>> &favorable,
           std::ifstream &train) {
  CsvReader reader(train);

  RowMap row;
  while (reader.next(row)) {
    std::string row_key = get_row_key(row);
    possible[row_key] += 1;
    favorable[row_key][row["Category"]] += 1;
  }
}

void predict(std::map<std::string, int> &possible,
             std::map<std::string, std::map<std::string, int>> &favorable,
             std::ifstream &test,
             std::ofstream &predicted) {
  std::array<std::string, 39> categories = {"ARSON", "ASSAULT", "BAD CHECKS", "BRIBERY",
                                            "BURGLARY", "DISORDERLY CONDUCT", "DRIVING UNDER THE INFLUENCE",
                                            "DRUG/NARCOTIC", "DRUNKENNESS", "EMBEZZLEMENT", "EXTORTION",
                                            "FAMILY OFFENSES", "FORGERY/COUNTERFEITING", "FRAUD",
                                            "GAMBLING", "KIDNAPPING", "LARCENY/THEFT", "LIQUOR LAWS",
                                            "LOITERING", "MISSING PERSON", "NON-CRIMINAL", "OTHER OFFENSES",
                                            "PORNOGRAPHY/OBSCENE MAT", "PROSTITUTION",
                                            "RECOVERED VEHICLE", "ROBBERY", "RUNAWAY", "SECONDARY CODES",
                                            "SEX OFFENSES FORCIBLE", "SEX OFFENSES NON FORCIBLE",
                                            "STOLEN PROPERTY", "SUICIDE", "SUSPICIOUS OCC", "TREA",
                                            "TRESPASS", "VANDALISM", "VEHICLE THEFT", "WARRANTS", "WEAPON LAWS"};
  // header
  predicted << "Id";
  for (size_t i = 0; i < categories.size(); ++i) {
    predicted << "," << categories[i];
  }
  predicted << std::endl;

  CsvReader reader(test);

  RowMap row;
  while (reader.next(row)) {
    predicted << row["Id"];
    std::string row_key = get_row_key(row);
    for (size_t i = 0; i < categories.size(); ++i) {
      predicted << "," << (static_cast<long double>(favorable[row_key][categories[i]]) /
                           possible[row_key]);
    }
    predicted << std::endl;
  }
}

int main() {
  std::map<std::string, int> possible;
  std::map<std::string, std::map<std::string, int>> favorable;
  std::ifstream train_f("/home/martin/Documents/repos/datos/entrega/trainFilteredSinBinarizarV3-columnas.csv");
  std::ifstream test("/home/martin/Documents/repos/datos/entrega/testFilteredSinBinarizarV3-columnas.csv");
  std::ofstream predicted("/media/martin/MARTIN/predicted.csv");

  train(possible, favorable, train_f);
  predict(possible, favorable, test, predicted);

  return 0;
}
