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
    /* ValueTypes */

    __RawString ValueTypes::none_()
    {
        return "NoneType";
    }

    __RawString ValueTypes::bool_()
    {
        return "bool";
    }

    __RawString ValueTypes::float_()
    {
        return "float";
    }

    __RawString ValueTypes::int_()
    {
        return "int";
    }

    /* any */

    any::any()
    {
        this->__value = 0;
        this->__type = ValueTypes::none_();
    }

    any::any(Object *value)
    {
        this->__value = (u64)(value);
        this->__type = "object";
    }

    any::any(Float *value)
    {
        this->__value = (u64)(value->__unbox__());
        this->__type = "float";
    }

    any::any(Int *value)
    {
        this->__value = (u64)(value->__unbox__());
        this->__type = "int";
    }

    /* Object */

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

    /* Float */

    Float::Float() : Float(0.0) {}

    Float::Float(double value)
    {
        this->__value = value;
    }

    Float::~Float()
    {
        this->__value = (f64)(0x0000000000000000);
    }

    Float::operator f64 *()
    {
        return &(this->__value);
    }

    Float::operator f64()
    {
        return this->__value;
    }

    f64 Float::__unbox__()
    {
        return (f64)(*this);
    }

    /* Int */

    Int::Int() : Int(0) {}

    Int::Int(i32 value)
    {
        this->__value = value;
    }

    Int::~Int()
    {
        this->__value = (i32)(0x00000000);
    }

    Int::operator i32 *()
    {
        return &(this->__value);
    }

    Int::operator i32()
    {
        return this->__value;
    }

    i32 Int::__unbox__()
    {
        return (i32)(*this);
    }
}

#endif // DRATINI_FOOTER
