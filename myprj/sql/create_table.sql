create table todos (
    todoId UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    contents TEXT,
    userId UUID DEFAULT gen_random_uuid()
);