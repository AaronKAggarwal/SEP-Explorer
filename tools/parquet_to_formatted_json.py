import pyarrow.parquet as pq
import json

def extract_fields_from_parquet(file_path, output_file):
    table = pq.read_table(file_path)
    documents = []

    for record_batch in table.to_batches():
        for i in range(record_batch.num_rows):
            shorturl = record_batch['shorturl'][i].as_py()
            title = record_batch['title'][i].as_py()
            pubinfo = record_batch['pubinfo'][i].as_py()
            preamble = record_batch['preamble'][i].as_py()
            toc = record_batch['toc'][i].as_py()
            main_text = record_batch['main_text'][i].as_py()
            bibliography = record_batch['bibliography'][i].as_py()
            related_entries = record_batch['related_entries'][i].as_py()

            document = {
                'shorturl': shorturl,
                'title': title,
                'pubinfo': pubinfo,
                'preamble': preamble,
                'toc': toc,
                'main_text': main_text,
                'bibliography': bibliography,
                'related_entries': related_entries,
            }
            documents.append(document)

    with open(output_file, 'w') as file:
        json.dump(documents, file, indent=4)

    print(f"Extracted data saved to {output_file}")


parquet_file = 'data/Stanford Plato.parquet'
output_file = 'data/Stanford Plato with all data.json'
extract_fields_from_parquet(parquet_file, output_file)
