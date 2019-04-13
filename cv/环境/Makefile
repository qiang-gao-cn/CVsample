a:
	clang++ m3u8_parse.cpp -o m3u8_parse -lcurl

b:
	clang++ M3U8Rec.cpp -o M3U8Rec

dep:
	curl -LOk https://raw.githubusercontent.com/kazuho/picojson/master/picojson.h

format:
	clang-format -style=Google -i M3U8Rec.cpp

check:
	cppcheck --enable=all m3u8_parse.cpp
	cpplint m3u8_parse.cpp
