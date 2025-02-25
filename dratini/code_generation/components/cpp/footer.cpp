#if !defined(dratini_FOOTER_CPP)
#define dratini_FOOTER_CPP

#include "header.cpp"

namespace dratini
{
    Object::Object()
    {
        // Create an attribute map for the object.
        // this->__attributes = new __RawDict();
    }

    Object::~Object()
    {
        this->__delete_raw_dict();
    }

    NoneType Object::__delete_raw_dict()
    {
        // // If this object has an attribute map:
        // if (this->__attributes != nullptr)
        // {
        //     // Delete the object's attribute map.
        //     delete this->__attributes;
        // }

        // return None;
    }
}

#endif // dratini_FOOTER_CPP
