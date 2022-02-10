mkdir -p ~/.streamlit

echo "\
[server]\n\
port = $PORT\n\n
enableCORS = false\n\n
headless = true\n\
\n\
" > ~/.streamlit/config.toml
