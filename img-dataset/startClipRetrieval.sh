#!/bin/bash
echo '{example_index: diffusiondbIndex}' > indices_paths.json
clip-retrieval back --port 1234 --indices-paths indices_paths.json --clip_model=ViT-L/14  --provide_aesthetic_embeddings True
