package sample;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.util.Set;

public class test {
    public static void main(String[] args)
    {
        String line = "{\"request\": false, \"type\": \"gameBoardFirst\", \"yourColor\": \"Red\", \"currentPlayer\": \"\\\"Red\\\"\", \"board\": \"[{\\\"Purple\\\": {\\\"currentTile\\\": [5, 4], \\\"ownedTiles\\\": [[5, 4]]}}, {\\\"Green\\\": {\\\"currentTile\\\": [4, 5], \\\"ownedTiles\\\": [[4, 5]]}}, {\\\"Red\\\": {\\\"currentTile\\\": [2, 1], \\\"ownedTiles\\\": [[2, 1], [2, 3]]}}]\"}";
       // String line = "{\"request\": false, \"type\": \"gameBoardFirst\", \"yourColor\": \"Red\", \"currentPlayer\": \"\\\"Red\\\"\", \"board\": \"[[\\\"Red\\\", [2, 5], [[2, 5]]], [\\\"Green\\\", [1, 5], [[1, 5]]], [\\\"Pink\\\", [3, 2], [[3, 2]]]]\"}";
        JSONParser parser = new JSONParser();
        try {

            JSONObject json = (JSONObject) parser.parse(line);
            Boolean request = (Boolean) json.get("request");
            String myColor = (String) json.get("yourColor");
            String board = (String) json.get("board");
            JSONArray boardArr = (JSONArray) parser.parse(board);

            for( Object x : boardArr)
            {
                JSONObject data = (JSONObject) x;
                Set keys = data.keySet();

                for(Object key : keys)
                {
                    JSONObject tiles = (JSONObject) data.get(key);
                    JSONArray curentTile = (JSONArray) tiles.get("currentTile");
                    JSONArray ownedTiles = (JSONArray) tiles.get("ownedTiles");

                    for(Object pos : ownedTiles)
                    {
                        JSONArray cords = (JSONArray) pos;
                     //   System.out.println(cords.get());
                    }

                }


            }


        } catch (ParseException e) { }


       // System.out.println(line);


    }

}
