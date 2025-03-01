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
