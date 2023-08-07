const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3000;

const pool = new Pool({
    user: 'postgres',
    host: 'db.fesgpwzjkedykiwpmatt.supabase.co',
    database: 'postgres',
    password: '17agustus2023',
    port: 5432,
});

app.use(cors());
app.use(express.json());

app.post('/api/data', async (req, res) => {
  try {
      const { polygon, startDate, endDate } = req.body.requestData;  // Updated to get startDate and endDate
      if (!polygon) {
          throw new Error('Polygon is required');
      }
      console.log(polygon)
      const polygonJSON = JSON.parse(polygon);
              
      const coordinates = polygonJSON.geometry.coordinates[0];
      const wktCoordinates = coordinates.map(coord => coord.join(" ")).join(",");
      console.log(wktCoordinates)
      const wkt = `POLYGON((${wktCoordinates}))`;
        
      // Convert GeoJSON to EWKB
      const ewkbQuery = `
        SELECT ST_AsEWKB(ST_SetSRID(ST_GeomFromText($1), 4326)) AS ewkb
      `;
        
      const ewkbResult = await pool.query(ewkbQuery, [wkt]);
      const convertedPolygon = ewkbResult.rows[0].ewkb;
      console.log (convertedPolygon)
      console.log (startDate)
      console.log (endDate)
       
      // Execute a SQL query to retrieve data within the geometry and date range
      const query = `
          SELECT *
          FROM spasial_data_training_site
          WHERE ST_Intersects(geom, ST_GeomFromEWKB($1))
          AND date BETWEEN $2 AND $3
      `; // Added a date filter

      const result = await pool.query(query, [convertedPolygon, startDate, endDate]); // Updated to include startDate and endDate

      console.log(result)
      res.json(result.rows);
  } catch (error) {
      console.error('Error retrieving data:', error);
      res.status(500).json({ error: 'An error occurred while retrieving data' });
  }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
