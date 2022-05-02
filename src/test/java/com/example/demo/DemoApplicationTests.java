package com.example.demo;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class DemoApplicationTests {

	@Test
	void contextLoads() {
		String a = "hello"
		String b = "hello"
		a.equals(b)
		b.equals(a)
		String c = "world"
		a.equals(c)
	}


}
