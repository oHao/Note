<template>
  <section class="real-App">
      <input type="text"
            placeholder="接下来要做什么？"
            autofocus='autofocus'
            @keyup.enter="addTodo"
            class="add-input"
      >
    <Item 
    v-for="todo in filtedTodos"
    :key="todo.id"
    :todo="todo"
    @del='deleteTodo'></Item>
    <tabs :filter="filter" :todos="todos" @toggle="toggle" @clearAllCompleted="clearAllCompleted"></tabs>
  </section>
</template>
<script>
import Item from '../todo/item.vue'
import tabs from '../todo/tabs.vue'
let cruTodos
let id=0
    export default {
        data(){
            return {
                todos: [],
                filter: "all"
            }
        },
        computed:{
            filtedTodos(){
                if(this.filter==='all'){
                    return this.todos
                }
                const iscompleted = this.filter==='completed'
                return this.todos.filter(todo=>todo.completed===iscompleted)
            }
        },
        components:{
            Item,
            tabs,
        },
        methods:{
            addTodo(e){
                this.todos.unshift(
                    {
                        id:id++,
                        content:e.target.value.trim(),
                        completed: false
                    }
                )
                e.target.value=''
            },
            deleteTodo(id){
                this.todos.splice(this.todos.findIndex(todo=>todo.id===id),1);
            },
            toggle(state){
                this.filter = state
                
            },
            clearAllCompleted(){
              this.todos =  this.todos.filter(todo=>!todo.completed)
            }
        }
    }
</script>
<style lang="stylus" scoped>
    .real-app {
        width 600px
        margin 0 auto
        box-shadow 0 0 5px #666
    }
    .add-input {
        position: relative;
        margin: 0;
        width: 100%;
        font-size: 24px;
        font-family: inherit;
        font-weight: inherit;
        line-height: 1.4em;
        border: 0;
        outline: none;
        color: inherit;
        box-sizing: border-box;
        font-smoothing: antialiased;
        padding: 16px 16px 16px 36px;
        border: none;
        box-shadow: inset 0 -2px 1px rgba(0, 0, 0, 0.03);
    }
</style>