import processing.serial.*;
import http.requests.*;

Serial myPort;
Table dataTable;
PrintWriter output;

int numReadings = 500;
int readingCounter = 0;
String product_id = "banana";
float previousVal = 0;
String fileName;

void setup() {
  String portName = Serial.list()[0];
  myPort = new Serial(this, portName, 9600);
  dataTable = new Table();
  output = createWriter("voltage_values.csv");
  println("start");
  processData(myPort);
  keyPressed();
}

void processData(Serial myPort) {
  while (true) {
    if (myPort.available() > 0) {
      // read value from Serial
      String val = myPort.readStringUntil('\n');
      val = trim(val);
      // print value to data table
      output.println(val);
      // make request if value is not null and different from previous
      if (val != null && float(val) != previousVal) {
        String request = "http://localhost:8080/" + product_id + "/set-light/" + val;
        PostRequest post = new PostRequest(request);
        post.send();
        previousVal = float(val);
      }
      //readingCounter++;
      //if (readingCounter > 50) {
      //  keyPressed();
      //}
    }
  }
}

void keyPressed() {
  output.flush(); // Writes the remaining data to the file
  output.close(); // Finishes the file
  exit(); // Stops the program
}
