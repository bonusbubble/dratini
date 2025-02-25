#if !defined(dratini_HEADER_CPP)
#define dratini_HEADER_CPP

#include <string>
#include <unordered_map>
#include <vector>

namespace dratini
{
    class Object;

    class Class;

    class Bool;
    class Float;
    class Int;
    class NoneType;
    class Str;

    using __RawDict = std::unordered_map<Object, Object>;
    using __RawList = std::vector<Object>;
    using __RawString = std::string;

    const NoneType None;

    class Class : Object
    {
    public:
        Class();
        ~Class();
    private:
        __RawString __name;
    };

    class Object
    {
    public:
        Class __class__;
        Dict __dict__;
        Object();
        ~Object();
        Class __class__();
        NoneType __del__();
        NoneType __delattr__();
        NoneType __delete__();
        Dict __dict__();
        Str __dir__();
        Bool __eq__();
        NoneType __init__();
        Int __hash__();
        Str __repr__();
        Int __sizeof__();
        Str __str__();
    private:
        __RawDict __attributes;
        NoneType __delete_raw_dict();
    };

    class Dict : Object
    {
    public:
        Dict();
        Dict(__RawDict data);
        Dict(__RawDict data);
        Dict(void *data);
        Dict(__RawDict *data);
        ~Dict();
    private:
        __RawDict *__data;
    };

    class NoneType : Object
    {
        Str __str__();
    };

    class Bool : Object
    {
    public:
        Bool();
        Bool(bool value);
        ~Bool();
    private:
        bool __value;
    };

    class Float : Object
    {
    public:
        Float();
        Float(float value);
        ~Float();
    private:
        float __value;
    };

    class Int : Object
    {
    public:
        Int();
        Int(int value);
        ~Int();
    private:
        int __value;
    };

    class Str : Object
    {
    public:
        Str();
        Str(std::string value);
        Str(const char *value);
        ~Str();
    private:
        std::string __value;
    };
}

#endif // dratini_HEADER_CPP
