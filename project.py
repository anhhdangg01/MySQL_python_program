import sys
import parserFunctions


def command_parser():
    """
    Parses the command retrieved from the command line.
    
    """
    command_input = sys.argv[1:]

    if command_input[0] == "import":
        parserFunctions.importParser(command_input[1])
    elif command_input[0] == "insertViewer":        
        parserFunctions.insertViewerParser(command_input[1], command_input[2], command_input[3], command_input[4],
                                           command_input[5], command_input[6], command_input[7], command_input[8],
                                           command_input[9], command_input[10], command_input[11], command_input[12])
    elif command_input[0] == "addGenre":
        parserFunctions.addGenreParser(command_input[1], command_input[2])
    elif command_input[0] == "deleteViewer":
        parserFunctions.deleteViewerParser(command_input[1])
    elif command_input[0] == "insertMovie":
        parserFunctions.insertMovieParser(command_input[1], command_input[2])
    elif command_input[0] == "insertSession":
        parserFunctions.insertSessionParser(command_input[1], command_input[2], command_input[3], command_input[4],
                                            command_input[5], command_input[6], command_input[7], command_input[8])
    elif command_input[0] == "updateRelease":
        parserFunctions.updateReleaseParser(command_input[1], command_input[2])
    elif command_input[0] == "listReleases":
        parserFunctions.releasesReviewedParser(command_input[1])
    elif command_input[0] == "popularRelease":
        parserFunctions.popularReleaseParser(command_input[1])
    elif command_input[0] == "releaseTitle":
        parserFunctions.releaseTitleParser(command_input[1])
    elif command_input[0] == "activeViewer":
        parserFunctions.activeViewersParser(command_input[1], command_input[2], command_input[3])
    elif command_input[0] == "videosViewed":
        parserFunctions.viewedVideosParser(command_input[1])


if __name__ == '__main__':
    command_parser()
