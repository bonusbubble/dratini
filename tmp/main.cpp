#include <iostream>

#include "../dratini/code_generation/components/cpp/header.cpp"

using namespace dratini;


template <typename Arg1>
void print(Arg1 message)
{
    std::cout << message << std::endl;
}


int main(int argc, char const *argv[])
{
    print("Hello, world!");
    print(3);

    return 0;
}


#include "../dratini/code_generation/components/cpp/footer.cpp"
