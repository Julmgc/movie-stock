## <font size="7">**Movie-stock**</font>

​### <font color="gree"> CRUD API for movies, using MongoDB </font> Saves a movie

## <font size="6">Base URL /api </font>

## <font size="6">Routes</font>

​
​

### <font color="gree"> POST </font> Saves a movie

​

```json
/movies
```

<font color="caramel"> _Request_ </font>
​

```json
{
  "movie": "Mary Poppins",
  "released_date": "01/02/1955",
  "rating": 2
}
```

​
<font color="yellow"> _Response_ </font>
​

```json
{
  "id": 1,
  "movie": "Mary Poppins",
  "rating": 2,
  "released_date": "1955-02-01"
}
}
```

​

### <font color="green"> GET </font> Shows all movies

​

```json
/movies
```

​
<font color="yellow"> _Response_ </font>
​

```json
{
  "data": [
    {
      "id": 1,
      "movie": "Mary Poppins",
      "rating": 2,
      "released_date": "Tue, 01 Feb 1955 00:00:00 GMT"
    },
    {
      "id": 2,
      "movie": "Peter Pan",
      "rating": 10,
      "released_date": "Mon, 01 Feb 1965 00:00:00 GMT"
    }
  ]
}
```

### <font color="purple"> GET </font> Returns a specific movie

​

```json
/movies/<int:id>
```

<font color="yellow"> _Response_ </font>
​

```json
{
  "data": [
    {
      "id": 1,
      "movie": "Mary Poppins",
      "rating": 2,
      "released_date": "Tue, 01 Feb 1955 00:00:00 GMT"
    }
  ]
}
```

​

### <font color="orange"> PATCH </font> Updates a spefic movie

​

```json
/movies/<int:id>
```

​
<font color="caramel"> Request </font>
​

```json
{
	"movie": "Mary Poppins""
}
```

​
<font color="yellow"> _Response_ </font>
​

```json
{
  "id": 1,
  "movie": "Mary Poppins",
  "rating": 10,
  "released_date": "1955-02-01"
}
```

### <font color="red"> DELETE </font> Delete a specific movie

​

```json
/movies/<int:id>
```

<font color="yellow"> _Response_ </font>
​

```json
NO CONTENT, 204
```

​
