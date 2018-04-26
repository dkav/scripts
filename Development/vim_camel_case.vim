" Key mappings to convert camelCase words to snake_case
" From - http://vim.wikia.com/wiki/Converting_variables_to_or_from_camel_case

" Find camelCase words
nnoremap <leader>c /\C\(\<\u[a-z0-9]\+\<Bar>[a-z0-9]\+\)\(\u\)<cr>

" Convert camelCase to snake_case
nnoremap <leader>s :,$s#\C\(\<\u[a-z0-9]\+\<Bar>[a-z0-9]\+\)\(\u\)#\l\1_\l\2#gc<cr>
