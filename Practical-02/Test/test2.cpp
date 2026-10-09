#include <iostream>

int main() {
	int number;
	std::cout << "Enter a number: ";
	std::cin >> number;

	if (number % 2 == 0) {
		std::cout << "Even\n";
	} else {
		std::cout << "Odd\n";
	}

	return 0;
}
