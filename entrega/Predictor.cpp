#include <limits>
#include "Predictor.h"
#include "CsvReader.h"

#define THRESHOLD 0.00008


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
    favorable[row_key][row.at("Category")] += 1;
  }

  for (std::map<std::string, int>::iterator it = possible.begin();
       it != possible.end(); ++it) {
    long unsigned int below_threshold = 0;
    
    for (size_t i = 0; i < categories.size(); ++i) {
      if (it->second > 0) {
        long double prob = static_cast<long double>(favorable[it->first][categories[i]]) / it->second;
        probabilities[it->first][categories[i]] = prob;
        if (prob < THRESHOLD) {
          below_threshold += 1;
        }
      } else {
        probabilities[it->first][categories[i]] = 0;
        below_threshold += 1;
      }
    }

    long double X = static_cast<long double>(THRESHOLD * it->second) /
                    (1 - THRESHOLD);
    for (size_t i = 0; i < categories.size(); ++i) {
      if (it->second > 0) {
        int fav = favorable[it->first][categories[i]];
        long double prob = fav / (it->second + X);
        if (prob < THRESHOLD) {
          probabilities[it->first][categories[i]] = X / (it->second + X);
        } else {
          probabilities[it->first][categories[i]] = prob;
        }
      } else {
        probabilities[it->first][categories[i]] = static_cast<long double>(1) / categories.size();
      }
    }
  }
}

void Predictor::predict(std::istream &test, std::ostream &predicted) {
  predicted.precision(std::numeric_limits<long double>::max_digits10);
  predicted << std::fixed;

  // header
  predicted << "Id";
  for (size_t i = 0; i < categories.size(); ++i) {
    predicted << "," << categories[i];
  }
  predicted << "\n";

  CsvReader reader(test);

  RowMap row;
  while (reader.next(row)) {
    predicted << row.at("Id");
    std::string row_key = get_row_key(row);
    for (size_t i = 0; i < categories.size(); ++i) {
      predicted << "," << probabilities[row_key][categories[i]];
    }
    predicted << "\n";
  }
}

std::string Predictor::get_row_key(RowMap &row) {
  return row.at("Zipcode") += row.at("DayLightCivil") += row.at("CrimeAsociationDual");
}
