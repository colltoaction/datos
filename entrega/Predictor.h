#ifndef ENTREGA_PREDICTOR_H
#define ENTREGA_PREDICTOR_H


#include <iosfwd>
#include <map>
#include <string>

class Predictor {
 public:
  /**
   * Entrena el modelo usando el stream train, que debe contener los datos en formato
   * csv delimitado por comas y sin comillas delimitadoras.
   */
  void train(std::istream &train);

  void predict(std::istream &test, std::ostream &predicted);

 private:
  static const std::array<std::string, 39> categories;
  std::map<std::string, std::map<std::string, long double>> probabilities;
  std::string get_row_key(std::map<std::string, std::string> &row);
};


#endif  // ENTREGA_PREDICTOR_H
