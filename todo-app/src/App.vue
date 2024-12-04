<script setup>
import { ref, onMounted } from "vue";

const todos = ref([]);

// Load todos from localStorage
onMounted(() => {
  const savedTodos = localStorage.getItem("todos");
  if (savedTodos) {
    todos.value = JSON.parse(savedTodos);
  }
});

// Save todos to localStorage whenever they change
function saveTodos() {
  localStorage.setItem("todos", JSON.stringify(todos.value));
}

// Add new todo
const newTodoText = ref("");
function addTodo() {
  if (newTodoText.value.trim()) {
    todos.value.push({
      id: Date.now(),
      text: newTodoText.value,
      done: false,
      dueDate: null
    });
    newTodoText.value = "";
    saveTodos();
  }
}

// Remove todo
function removeTodo(id) {
  todos.value = todos.value.filter(todo => todo.id !== id);
  saveTodos();
}

// Toggle todo completion
function toggleTodo(id) {
  const todo = todos.value.find(todo => todo.id === id);
  if (todo) {
    todo.done = !todo.done;
    saveTodos();
  }
}

// Update todo text
function updateTodoText(id, newText) {
  const todo = todos.value.find(todo => todo.id === id);
  if (todo && newText.trim()) {
    todo.text = newText;
    saveTodos();
  }
}

// Set todo due date
function setDueDate(id, date) {
  const todo = todos.value.find(todo => todo.id === id);
  if (todo) {
    todo.dueDate = date;
    saveTodos();
  }
}
</script>

<template>
  <div class="todo-app">
    <h1>Todo List</h1>
    
    <!-- Add new todo -->
    <div class="add-todo">
      <input 
        v-model="newTodoText"
        @keyup.enter="addTodo"
        placeholder="Add new todo"
        data-test="new-todo-input"
      >
      <button @click="addTodo" data-test="add-todo-button">Add</button>
    </div>

    <!-- Todo list -->
    <ul class="todo-list">
      <li v-for="todo in todos" :key="todo.id" :class="{ done: todo.done }">
        <!-- Checkbox -->
        <input 
          type="checkbox"
          v-model="todo.done"
          :data-test="`todo-checkbox-${todo.id}`"
        >
        
        <!-- Todo text -->
        <input 
          type="text"
          v-model="todo.text"
          :data-test="`todo-text-${todo.id}`"
        >
        
        <!-- Due date -->
        <input 
          type="date"
          v-model="todo.dueDate"
          :data-test="`todo-date-${todo.id}`"
        >
        
        <!-- Delete button -->
        <button 
          @click="removeTodo(todo.id)"
          :data-test="`remove-todo-${todo.id}`"
        >
          Delete
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.todo-app {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.add-todo {
  margin-bottom: 20px;
}

.add-todo input {
  padding: 8px;
  margin-right: 10px;
}

.todo-list {
  list-style: none;
  padding: 0;
}

.todo-list li {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 5px;
  background: #f5f5f5;
  border-radius: 4px;
}

.todo-list li.done {
  background: #e0e0e0;
  text-decoration: line-through;
}

.todo-list li input[type="checkbox"] {
  margin-right: 10px;
}

.todo-list li input[type="text"] {
  flex-grow: 1;
  margin: 0 10px;
  padding: 5px;
}

.todo-list li input[type="date"] {
  margin: 0 10px;
}

button {
  padding: 8px 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #45a049;
}
</style>
