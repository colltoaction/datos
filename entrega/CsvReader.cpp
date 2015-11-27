#include <iosfwd>
#include <sstream>
#include <string>
#include <vector>
#include "CsvReader.h"


CsvReader::CsvReader(std::istream &input)
  : input_(input) {
  std::string line;
  if (!std::getline(input_, line)) {
    throw std::runtime_error("The input is empty");
  }

  // save headers and their index in the csv file
  std::vector<std::string> header_tokens = split_line(line);
  for (unsigned int i = 0; i < header_tokens.size(); ++i) {
    headers_[i] = header_tokens[i];
  }
}

bool CsvReader::next(RowMap &row) {
  std::string line;
  if (!std::getline(input_, line)) {
    return false;
  }

  // map tokens to keys
  std::vector<std::string> tokens = split_line(line);
  for (std::map<int, std::string>::iterator it = headers_.begin();
       it != headers_.end(); it++) {
    row[it->second] = tokens[it->first];
  }

  return true;
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
