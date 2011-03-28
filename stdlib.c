#include <syscall.h>

void writeint(int num) {
	char buf[20];
	char result[20] = "0\n";
	char *pos = buf;
	char *writeptr = result;
	int numWritten;

	// Handle negative numbers
	if (num < 0) {
		*writeptr++ = '-';
		num = -num;
	}
  
	if (num > 0) {
		// Build the number in reverse order
		while (num > 0) {
			*pos++ = (num % 10) + '0';
			num /= 10;
		}
		pos--;

		// Now we need to copy the results into the output buffer, reversed
		while (pos > buf) {
			*writeptr++ = *pos--;
		}
		*writeptr++ = *pos;
		*writeptr++ = 10;
		*writeptr++ = 0;
	}
	else {
		// number is 0; use default result
		writeptr = result + 3;
	}
  
	write(1, result, (writeptr - result) - 1);
}

int readint(void) {
	char buf[20];     //number buffer
	int num_cur = 0;  //current digit being converted
	int num_read = 0; //result value
	int num_mult = 1; //multiply result by this value (used for negative numbers)
	int npow = 1;     //calculate powers for digits
	int x = 0, y = 0; //loop values
	int len = 0;      //len returned by read()

	len = read(0, buf, 20);
	if (len == -1) { //error on read
		return num_read; //just return a zero
	}
	--len; //get rid of newline

	if (buf[0] == '-') { //check for negative number
		num_mult = -1; //result will be negative
		x = 1;         //loop value starts at 1 now instead of 0
	}

	for (;x < len; ++x) {
		num_cur = buf[x] - 48; //convert ascii digit to integer
		npow = 1;
		y = (len - x);
		for (;y > 1; --y) { //get power of 10 for digit place
			npow *= 10;
		}
		num_read += (num_cur * npow); //add place value to total
	}

	return num_read * num_mult;
}

