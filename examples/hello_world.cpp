#if !defined(DRATINI_HEADER)
#define DRATINI_HEADER

#include <cmath>
#include <string>
#include <unordered_map>
#include <vector>

extern "C" {
    #include <bgc.h>
    #include <raylib.h>
}

namespace dratini
{
    class Object;

    // class Class;

    // class Bool;
    // class Float;
    // class Int;
    // class NoneType;
    // class Str;

    using __RawValue = uint64_t;

    using __RawDict = std::unordered_map<__RawValue, Object *>;
    // using __RawList = std::vector<Object>;
    // using __RawString = std::string;

    // class Dict;
    // class List;

    class Object
    {
    public:
        // Class *__class__;
        // Dict *__dict__;
        Object();
        ~Object();
        void __del__();
        void __delattr__();
        void __delete__();
        // Str *__dir__();
        bool __eq__();
        void __init__();
        int __hash__();
        // Str *__repr__();
        int __sizeof__();
        // Str *__str__();
    private:
        __RawDict *__attributes;
        __RawDict * __create_raw_dict();
        void __delete_raw_dict();
        void __initialize_attributes();
    };

    // class Class : Object
    // {
    // public:
    //     Class();
    //     ~Class();
    // private:
    //     __RawString __name;
    // };

    // class NoneType : Object
    // {
    //     Str __str__();
    // };

    // const NoneType None;

    // class Dict : Object
    // {
    // public:
    //     Dict();
    //     Dict(void *attributes);
    //     Dict(__RawDict *attributes);
    //     ~Dict();
    // };

    // class Bool : Object
    // {
    // public:
    //     Bool();
    //     Bool(bool value);
    //     ~Bool();
    // private:
    //     bool __value;
    // };

    // class Float : Object
    // {
    // public:
    //     Float();
    //     Float(float value);
    //     ~Float();
    // private:
    //     float __value;
    // };

    // class Int : Object
    // {
    // public:
    //     Int();
    //     Int(int value);
    //     ~Int();
    // private:
    //     int __value;
    // };

    // class Str : Object
    // {
    // public:
    //     Str();
    //     Str(std::string value);
    //     Str(const char *value);
    //     ~Str();
    // private:
    //     std::string __value;
    // };
}

#define dratini__new(T)     new (bgc_malloc_ext(BGC_GLOBAL_GC, sizeof(T), ([](void *this_){ std::destroy_at<T>((T *)(this_)); }))) T

#include <any>
#include <iostream>

void foo()
{
    std::any object = dratini__new(dratini::Object)();

    object = dratini__new(double)(3.14);
}

#endif // DRATINI_HEADER
int main() {
    bgcx_start();
    int screen_width = 800;
    int screen_height = 450;
    InitWindow(screen_width, screen_height, "Dratini App");
    SetTargetFPS(60);
    ;
    CloseWindow();
    bgcx_stop();
}
#if !defined(DRATINI_FOOTER)
#define DRATINI_FOOTER

extern "C" {
    #include <bgc.h>
}

#if !defined(DRATINI_HEADER)
#include "header.cpp"
#endif

#include <iostream>

namespace dratini
{
    Object::Object()
    {
        std::cout << "ctor" << std::endl;
        this->__initialize_attributes();
    }

    Object::~Object()
    {
        std::cout << "dtor" << std::endl;
        this->__delete_raw_dict();
    }

    void Object::__delete_raw_dict()
    {
        // If this object has an attribute map:
        if (this->__attributes != nullptr)
        {
            // Delete the object's attribute map.
            delete this->__attributes;
        }
    }

    __RawDict * Object::__create_raw_dict()
    {
        // Allocate a new managed `__RawDict`.
        // return dratini__new(__RawDict)();
        __RawDict *dict = new (malloc(sizeof(__RawDict))) __RawDict();
        // return new __RawDict();

        return dict;
    }

    void Object::__initialize_attributes()
    {
        // Create an attribute map for the object.
        this->__attributes = this->__create_raw_dict();
    }
}

#endif // DRATINI_FOOTER
