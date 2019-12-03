package sample;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.scene.Group;
import javafx.scene.Node;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.GridPane;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.scene.text.TextAlignment;
import javafx.stage.Stage;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Set;


public class Client extends Application {

    private static int[] curPos;

    private static Stage primaryStage;

    private static Button[][] btn;
    private static String[][] territory;

    private static String address = "127.0.0.1";
    private static int port = 255;
    private static int gridSize = 5;

    private static GridPane gridPane;

    private static Socket socket;
    private static DataOutputStream output;
    private static BufferedReader input;

    private static boolean myTurn = false;
    private static boolean gridSceneAlreadySet = false;



    private static void client() throws IOException {

        socket = new Socket(address, port);
        output = new DataOutputStream(socket.getOutputStream());
        input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

        while(true)
        {
            String line = input.readLine();

            if(line.equals("alive?")) output.writeBytes("yes");

            JSONParser parser = new JSONParser();
            try {

                System.out.println(line);

                JSONObject json = (JSONObject) parser.parse(line);
                Boolean request = (Boolean) json.get("request");
                String myColor = (String) json.get("yourColor");
                String board = (String) json.get("board");
                String type = (String) json.get("type");
                String currentPlayer = (String) json.get("currentPlayer");


                if (type.equalsIgnoreCase("move")) {
                    myTurn = true;
                    Platform.runLater(
                            () -> {
                                primaryStage.setTitle("My Turn");
                            }
                    );
                }

                else {
                    Platform.runLater(
                            () -> {
                                primaryStage.setTitle("Game Client");
                            }
                    );
                }

                if (board == null) return;

                JSONArray boardArr = (JSONArray) parser.parse(board);
                Long X = new Long(0);
                Long Y = new Long(0);;

                for (Object x : boardArr) {
                    JSONObject data = (JSONObject) x;
                    Set colors = data.keySet();

                    for (Object color : colors) {

                        JSONObject tiles = (JSONObject) data.get(color);
                        JSONArray curentTile = (JSONArray) tiles.get("currentTile");
                        JSONArray ownedTiles = (JSONArray) tiles.get("ownedTiles");

                        for (Object pos : ownedTiles) {

                            JSONArray coordinates = (JSONArray) pos;
                            X = (Long) coordinates.get(0) - 1;
                            Y = (Long) coordinates.get(1) - 1;
                            territory[X.intValue()][Y.intValue()] = (String) color;

                            if (color.equals(myColor)) {


                                X = (Long) curentTile.get(0) - 1;
                                Y = (Long) curentTile.get(1) - 1;

                                curPos = new int[]{X.intValue(), Y.intValue()};

                                String style = String.format("-fx-background-color: %s;\n", color)
                                        + "-fx-border-color: black;\n"
                                        + "-fx-border-insets: 5;\n"
                                        + "-fx-border-width: 3;\n"
                                        + "-fx-border-style: solid;\n";

                                btn[X.intValue()][Y.intValue()].setStyle(style);
                            }
                            else {

                                String style = String.format("-fx-background-color: %s;", color);
                                btn[X.intValue()][Y.intValue()].setStyle(style);
                            }
                        }

                    }
                }


                if(request != null && gridSceneAlreadySet == false)
                {
                    gridSceneAlreadySet = true;
                    Platform.runLater(
                            () -> {

                                Scene gridScene = new Scene(gridPane);
                                gridPane.setVisible(false);
                                primaryStage.setScene(gridScene);

                                gridPane.setVisible(true);
                            }
                    );
                }


            } catch (ParseException e) { }

        }
    }
    private double distance(int[] a, int[] b)
    {
        return Math.sqrt(Math.pow(b[0] - a[0], 2) + Math.pow(b[1] - a[1], 2));
    }


    @Override
    public void start(Stage primaryStage) throws Exception{

        this.primaryStage = primaryStage;

        primaryStage.setTitle("Game Client");
        gridPane = new GridPane();

        btn = new Button[gridSize][gridSize];
        territory = new String[gridSize][gridSize];

        for(int x = 0; x < gridSize; x++){
            for(int y =0; y < gridSize;y++){

                btn[x][y] = new Button();
                btn[x][y].setPrefSize(50, 50);
                btn[x][y].setOnMouseClicked(new EventHandler<MouseEvent>() {
                    @Override
                    public void handle(MouseEvent event) {
                        if (event.getClickCount() == 1)
                        {
                            Node source = (Node)event.getSource() ;
                            Integer x = GridPane.getColumnIndex(source);
                            Integer y = GridPane.getRowIndex(source);
                            System.out.printf("Clicked on [%d, %d]%n", x, y);
                            System.out.printf("Current Position [%d, %d]%n", curPos[0], curPos[1]);

                            double distance = distance(curPos, new int[]{x,y});
                            if(myTurn)
                            {

                                if (distance >= 1.0 && distance < 2.0)
                                {
                                    if(territory[x][y] == null) {

                                        try
                                        {
                                            String dir = "";
                                            if(y < curPos[1] && x == curPos[0])
                                            {
                                                dir = "UP";
                                            }
                                            if(y > curPos[1] && x == curPos[0])
                                            {
                                                dir = "DOWN";
                                            }
                                            if(x < curPos[1] && y == curPos[1])
                                            {
                                                dir = "LEFT";
                                            }
                                            if(x > curPos[1] && y == curPos[1])
                                            {
                                                dir = "RIGHT";
                                            }

                                            JSONObject move = new JSONObject();
                                            move.put("move", dir);
                                            output.write(move.toJSONString().getBytes("US-ASCII"));

                                        } catch (IOException e) { }
                                    }
                                    else {

                                        System.out.println("Invalid Move");
                                    }
                                }
                                else
                                {
                                    System.out.println("Invalid Move");
                                }
                            }
                            else
                            {
                                System.out.println("Not your turn");
                            }

                        }

                    }
                });
                gridPane.add(btn[x][y], x, y);

            }
        }

        Text lobbyText = new Text(210, 125, "Waiting for players...");

        lobbyText.setFont(new Font(20));
        Group root = new Group(lobbyText);

        Scene lobbyScene = new Scene(root, 600, 300);
        primaryStage.setScene(lobbyScene);

        primaryStage.show();

    }

    public static void main(String[] args) throws IOException {
        Thread thread = new Thread(){
            public void run(){
                try {
                    client();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        };

        thread.start();
        launch(args);


    }
}