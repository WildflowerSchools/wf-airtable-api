from pyairtable import api
from pyairtable.api.params import options_to_params


class Api(api.Api):
    def paginate(self, base_id: str, table_name: str, offset: None, **options):
        table = self.table(base_id=base_id, table_name=table_name)
        params = options_to_params(options)

        table_url = table.url  # .get_table_url(base_id, table_name)
        if isinstance(offset, str) and str.strip(offset) != "":
            params.update({"offset": str.strip(offset)})

        data = table.api.request("get", table_url, params=params)
        records = data.get("records", [])
        next_offset = data.get("offset", "")

        return records, next_offset
