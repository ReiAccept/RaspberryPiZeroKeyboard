key: key_report.o main.o
	g++ main.o key_report.o -lpthread -o key

key_report.o: key_report.cpp
	g++ -Wall -c key_report.cpp -o key_report.o

main.o: main.cpp
	g++ -Wall -c main.cpp -o main.o