package chat.Controllers;

import java.io.*;
import java.util.HashMap;
import java.util.Map;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private Process pythonProcess;
    private BufferedWriter pythonWriter;
    private BufferedReader pythonReader;

    public ChatController() throws IOException {
        // Démarrer le processus Python
        ProcessBuilder processBuilder = new ProcessBuilder(
            "python", 
            "src/main/java/chat/Python/main.py"
        );
        pythonProcess = processBuilder.start();

        // Initialiser les flux stdin et stdout
        pythonWriter = new BufferedWriter(new OutputStreamWriter(pythonProcess.getOutputStream()));
        pythonReader = new BufferedReader(new InputStreamReader(pythonProcess.getInputStream()));
    }

    @PostMapping
    public Map<String, String> chat(@RequestBody Map<String, String> payload) {
        String userInput = payload.get("message"); // Lire le message du corps JSON
        Map<String, String> response = new HashMap<>();

        try {
            // Envoyer l'entrée utilisateur au processus Python
            pythonWriter.write(userInput + "\n");
            pythonWriter.flush();

            // Lire la réponse du processus Python
            String output = pythonReader.readLine();

            // Ajouter la réponse au résultat
            response.put("botResponse", output);
        } catch (IOException e) {
            response.put("error", "Une erreur s'est produite : " + e.getMessage());
        }

        return response;
    }

    @Override
    protected void finalize() throws Throwable {
        super.finalize();
        if (pythonProcess != null) {
            pythonProcess.destroy();
        }
    }
}
