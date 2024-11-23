package main

import (
	"testing"
)

func TestExample(t *testing.T) {
	res := lookAndSay("1")
	if res != "11" {
		t.Errorf("1 should turn into 11, got: %s", res)
	}

	res = lookAndSay("11")
	if res != "21" {
		t.Errorf("11 should turn into 21, got: %s", res)
	}

	res = lookAndSay("111221")
	if res != "312211" {
		t.Errorf("111221 should turn into 312211, got: %s", res)
	}
}