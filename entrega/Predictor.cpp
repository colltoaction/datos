#include "Predictor.h"
#include "CsvReader.h"


const std::array<std::string, 39> Predictor::categories = {
    "ARSON", "ASSAULT", "BAD CHECKS", "BRIBERY",
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


void Predictor::train(std::istream &train) {
  CsvReader reader(train);

  std::map<std::string, int> possible;
  std::map<std::string, std::map<std::string, int>> favorable;
  RowMap row;
  while (reader.next(row)) {
    std::string row_key = get_row_key(row);
    possible[row_key] += 1;
    favorable[row_key][row["Category"]] += 1;
  }

  for (size_t i = 0; i < categories.size(); ++i) {
    for (std::map<std::string, int>::iterator it = possible.begin();
         it != possible.end(); ++it) {
      probabilities[it->first][categories[i]] =
          static_cast<long double>(favorable[it->first][categories[i]]) / it->second;
    }
  }
}

void Predictor::predict(std::istream &test, std::ostream &predicted) {
  // header
  predicted << "Id";
  for (size_t i = 0; i < categories.size(); ++i) {
    predicted << "," << categories[i];
  }
  predicted << "\n";

  CsvReader reader(test);

  RowMap row;
  while (reader.next(row)) {
    predicted << row["Id"];
    std::string row_key = get_row_key(row);
    for (size_t i = 0; i < categories.size(); ++i) {
      predicted << "," << probabilities[row_key][categories[i]];
    }
    predicted << "\n";
  }
}

std::string Predictor::get_row_key(RowMap &row) {
  return row["Zipcode"] += row["Daylight"] += row["CrimeAsociationDual"];
}
