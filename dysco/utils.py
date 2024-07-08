class AbstractScheduler:
    def __call__(self, iter, num_iters):
        raise NotImplemented

class SchedulableParameter:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self 
        else:
            return getattr(obj, self.private_name)

    def __set__(self, obj, val):
        if isinstance(val, int) or isinstance(val, float):
            setattr(obj, self.private_name, ConstantScheduler(val))
        elif isinstance(val, AbstractScheduler):
            setattr(obj, self.private_name, val)
        else:
            raise TypeError("An instance of a SchedulableParameter should "
                "extend AbstractScheduler.")

class ConstantScheduler(AbstractScheduler):
    def __init__(self, val):
        self.val = val
    
    def __call__(self, iter, num_iters):
        return self.val

class LinearScheduler(AbstractScheduler):
    def __init__(self, init_val, final_val):
        self.init_val = init_val
        self.final_val = final_val
    
    def __call__(self, iter, num_iters):
        if num_iters == 1:
            return self.init_val
        else:
            return self.init_val \
                + (self.final_val - self.init_val)/(num_iters-1)*iter