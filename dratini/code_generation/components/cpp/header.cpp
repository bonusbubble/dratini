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

const auto begin_drawing = BeginDrawing;
const auto clear_background = ClearBackground;
const auto close_window = CloseWindow;
const auto draw_text = DrawText;
const auto end_drawing = EndDrawing;
const auto init_window = InitWindow;
const auto set_target_fps = SetTargetFPS;
const auto window_should_close = WindowShouldClose;

namespace dratini
{
    class any;

    class Object;

    // class ClassType;

    // class Bool;
    class Float;
    class Int;
    // class NoneType;
    // class Str;

    using f64 = double;
    using f32 = float;
    using i8 = int8_t;
    using i16 = int16_t;
    using i32 = int32_t;
    using i64 = int64_t;
    using u8 = uint8_t;
    using u16 = uint16_t;
    using u32 = uint32_t;
    using u64 = uint64_t;

    using __RawValue = uint64_t;

    using __RawDict = std::unordered_map<__RawValue, Object *>;
    using __RawList = std::vector<Object>;
    using __RawString = std::string;

    // class Dict;
    // class List;

    class ValueTypes
    {
    public:
        static __RawString none_();
        static __RawString object_();
        static __RawString bool_();
        static __RawString float_();
        static __RawString int_();
    };

    class ClassType
    {
    public:
        ClassType();
        ~ClassType();
    private:
        __RawString __name;
    };

    class any
    {
    public:
        any();
        any(Object *object);
        any(Float *value);
        any(Int *value);
        operator bool();
        operator double();
        operator int();
        operator __RawString();
        operator Object *();
        __RawString __primitivetypename__();
    private:
        u64 __value;
        __RawString __type;
    };

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

    // class NoneType : public Object
    // {
    //     Str __str__();
    // };

    // const NoneType None;

    // class Dict : public Object
    // {
    // public:
    //     Dict();
    //     Dict(void *attributes);
    //     Dict(__RawDict *attributes);
    //     ~Dict();
    // };

    // class Bool : public Object
    // {
    // public:
    //     Bool();
    //     Bool(bool value);
    //     ~Bool();
    // private:
    //     bool __value;
    // };

    class Float : public Object
    {
    public:
        Float();
        Float(f64 value);
        ~Float();
        operator f64();
        operator f64 *();
        f64 __unbox__();
    private:
        f64 __value;
    };

    class Int : public Object
    {
    public:
        Int();
        Int(i32 value);
        ~Int();
        operator i32();
        operator i32 *();
        i32 __unbox__();
        Int bit_length();
    private:
        i32 __value;
    };

    // class Str : public Object
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

using namespace dratini;

void foo()
{
    any object = dratini__new(Object)();

    object = dratini__new(Float)(3.14);
}

#endif // DRATINI_HEADER
