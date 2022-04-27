from pyairtable import api


class Api(api.Api):
    def paginate(self, base_id: str, table_name: str, offset: None, **options):
        params = self._options_to_params(**options)

        table_url = self.get_table_url(base_id, table_name)
        if isinstance(offset, str) and str.strip(offset) != "":
            params.update({"offset": str.strip(offset)})

        data = self._request("get", table_url, params=params)
        records = data.get("records", [])
        next_offset = data.get("offset", "")

        return records, next_offset
