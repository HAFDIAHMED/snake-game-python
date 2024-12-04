import { mount } from '@vue/test-utils'
import { describe, it, expect, beforeEach } from 'vitest'
import App from '../App.vue'

describe('Todo App', () => {
  let wrapper;

  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();
    wrapper = mount(App);
  });

  it('adds a new todo', async () => {
    const input = wrapper.get('[data-test=new-todo-input]');
    await input.setValue('Test todo');
    await wrapper.get('[data-test=add-todo-button]').trigger('click');
    await wrapper.vm.$nextTick();

    const todos = wrapper.findAll('.todo-list li');
    expect(todos).toHaveLength(1);
    const todoId = todos[0].attributes('key');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();
    expect(wrapper.get(`[data-test=todo-text-${todoId}]`).element.value).toBe('Test todo');
  });

  it('marks a todo as done', async () => {
    // Add a todo first
    const input = wrapper.get('[data-test=new-todo-input]');
    await input.setValue('Test todo');
    await wrapper.get('[data-test=add-todo-button]').trigger('click');
    await wrapper.vm.$nextTick();

    // Get the todo's ID from the first todo item
    const todos = wrapper.findAll('.todo-list li');
    expect(todos).toHaveLength(1);
    const todoId = todos[0].attributes('key');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    // Toggle the todo
    const checkbox = wrapper.get(`[data-test=todo-checkbox-${todoId}]`);
    await checkbox.setValue(true);
    await checkbox.trigger('change');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    expect(wrapper.get('.todo-list li').classes()).toContain('done');
  });

  it('removes a todo', async () => {
    // Add a todo first
    const input = wrapper.get('[data-test=new-todo-input]');
    await input.setValue('Test todo');
    await wrapper.get('[data-test=add-todo-button]').trigger('click');
    await wrapper.vm.$nextTick();

    // Get the todo's ID from the first todo item
    const todos = wrapper.findAll('.todo-list li');
    expect(todos).toHaveLength(1);
    const todoId = todos[0].attributes('key');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    // Remove the todo
    await wrapper.get(`[data-test=remove-todo-${todoId}]`).trigger('click');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    const updatedTodos = wrapper.findAll('.todo-list li');
    expect(updatedTodos).toHaveLength(0);
  });

  it('updates todo text', async () => {
    // Add a todo first
    const input = wrapper.get('[data-test=new-todo-input]');
    await input.setValue('Test todo');
    await wrapper.get('[data-test=add-todo-button]').trigger('click');
    await wrapper.vm.$nextTick();

    // Get the todo's ID from the first todo item
    const todos = wrapper.findAll('.todo-list li');
    expect(todos).toHaveLength(1);
    const todoId = todos[0].attributes('key');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    // Update the todo text
    const todoInput = wrapper.get(`[data-test=todo-text-${todoId}]`);
    await todoInput.setValue('Updated todo');
    await todoInput.trigger('change');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    expect(todoInput.element.value).toBe('Updated todo');
  });

  it('sets a due date', async () => {
    // Add a todo first
    const input = wrapper.get('[data-test=new-todo-input]');
    await input.setValue('Test todo');
    await wrapper.get('[data-test=add-todo-button]').trigger('click');
    await wrapper.vm.$nextTick();

    // Get the todo's ID from the first todo item
    const todos = wrapper.findAll('.todo-list li');
    expect(todos).toHaveLength(1);
    const todoId = todos[0].attributes('key');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    // Set the due date
    const date = '2024-12-31';
    const dateInput = wrapper.get(`[data-test=todo-date-${todoId}]`);
    await dateInput.setValue(date);
    await dateInput.trigger('change');
    await wrapper.vm.$nextTick();
    await wrapper.vm.$nextTick();

    expect(dateInput.element.value).toBe(date);
  });

  it('persists todos in localStorage', async () => {
    // Add a todo
    const input = wrapper.get('[data-test=new-todo-input]');
    await input.setValue('Test todo');
    await wrapper.get('[data-test=add-todo-button]').trigger('click');
    await wrapper.vm.$nextTick();

    // Check localStorage
    const savedTodos = JSON.parse(localStorage.getItem('todos'));
    expect(savedTodos).toHaveLength(1);
    expect(savedTodos[0].text).toBe('Test todo');
  });
});
