#include <iosfwd>
#include <sstream>
#include <string>
#include <vector>
#include "CsvReader.h"


CsvReader::CsvReader(std::istream &input)
  : input_(input) {
  std::string line;
  if (std::getline(input_, line)) {
    std::vector<std::string> header_tokens = split_line(line);
    for (int i = 0; i < header_tokens.size(); ++i) {
      headers_[i] = header_tokens[i];
    }
  } else {
    throw std::runtime_error("The input is empty");
  }
}

bool CsvReader::next(RowMap &row) {
  std::string line;
  if (std::getline(input_, line)) {
    // map tokens to keys
    std::vector<std::string> tokens = split_line(line);
    for (std::map<int, std::string>::iterator it = headers_.begin();
         it != headers_.end(); it++)
      row[it->second] = tokens[it->first];
      return true;
  } else {
    return false;
  }
}

std::vector<std::string> CsvReader::split_line(std::string &line) {
  std::vector<std::string> result;

  std::stringstream lineStream(line);
  std::string cell;

  while (std::getline(lineStream, cell, ',')) {
    result.push_back(cell);
  }
  return result;
}
