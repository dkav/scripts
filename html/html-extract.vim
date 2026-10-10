" Reusable helpers for cleaning pasted HTML in the current buffer.
"
" Usage:
"   :ExtractByClass span JJmCi    " keep only the text of <span class="... JJmCi ...">
"   :ExtractByTag li              " keep only the text of every <li>
"   :StripTags                    " remove all tags, keep all text, one chunk per line
"
" Limits: element text must not contain nested tags (the text part is [^<]*).

function! s:Finish()
    silent! %s/@@//e
    silent! %s/&amp;/\&/ge
    silent! %s/&lt;/</ge
    silent! %s/&gt;/>/ge
    silent! %s/&quot;/"/ge
    silent! %s/&#39;/'/ge
    silent! %s/&nbsp;/ /ge
    silent! %s/\r//ge
    silent! %s/^\s\+\|\s\+$//ge
    silent! g/^\s*$/d
endfunction

function! ExtractByClass(tag, class)
    silent! %join
    let l:pat = '<' . a:tag . '[^>]*class="[^"]*\<' . a:class . '\>[^"]*"[^>]*>\([^<]*\)<\/' . a:tag . '>'
    execute 'silent! %s/' . l:pat . '/\r@@\1\r/g'
    silent! v/^@@/d
    silent! %s/^@@//
    call s:Finish()
endfunction

function! ExtractByTag(tag)
    silent! %join
    execute 'silent! %s/<' . a:tag . '\%(\s[^>]*\)\?>\([^<]*\)<\/' . a:tag . '>/\r@@\1\r/g'
    silent! v/^@@/d
    silent! %s/^@@//
    call s:Finish()
endfunction

function! StripTags()
    silent! %join
    silent! %s/<[^>]*>/\r/g
    call s:Finish()
endfunction

command! -nargs=+ ExtractByClass call ExtractByClass(<f-args>)
command! -nargs=1 ExtractByTag   call ExtractByTag(<f-args>)
command! StripTags               call StripTags()
