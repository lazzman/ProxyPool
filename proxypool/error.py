'异常模块'


class ResourceDepletionError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):  # __str__相当于java中Object的toString()方法，当print该对象时，会调用__str__方法
        # repr（）函数得到的字符串通常可以用来重新获得该对象，repr（）的输入对python比较友好。通常情况下obj==eval(repr(obj))这个等式是成立的。
        return repr('代理源已耗尽')


class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池暂无可用代理')
