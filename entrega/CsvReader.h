#ifndef ENTREGA_CSVREADER_H
#define ENTREGA_CSVREADER_H


#include <fstream>
#include <map>
#include <vector>

typedef std::map<std::string, std::string> RowMap;

class CsvReader {
 public:
  /**
   * Toma un stream input que debe contener datos en formato csv delimitado por comas,
   * con cabecera, y sin comillas delimitadoras.
   */
  CsvReader(std::istream &input);

  /**
   * Toma un mapa sobre el cual va a escribir los datos de la línea leída.
   * Retorna true si pudo leer correctamente o false en caso de encontrar
   * el final del archivo.
   */
  bool next(RowMap &row);

 private:
  std::istream &input;
  std::map<int, std::string> headers;
  std::vector<std::string> split_line(std::string &string);
};


#endif  // ENTREGA_CSVREADER_H
