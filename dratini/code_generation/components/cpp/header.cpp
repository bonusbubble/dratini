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
    class Object;

    using any = Object;

    // class ClassType;

    // class Bool;
    // class Float;
    // class Int;
    // class NoneType;
    // class Str;

    using __RawValue = uint64_t;

    using __RawDict = std::unordered_map<__RawValue, Object *>;
    using __RawList = std::vector<Object>;
    using __RawString = std::string;

    // class Dict;
    // class List;

    class ClassType
    {
    public:
        ClassType();
        ~ClassType();
    private:
        __RawString __name;
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
