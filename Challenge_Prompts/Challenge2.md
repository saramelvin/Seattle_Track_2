# Challenge 2: Contextualizing COLREGs Interactions

Having accurate models of the real-world behavior for ships is a valuable tool for preventing collisions for both manned and autonomous vessels. This challenge uses the AIS data to find patterns in vessel behavior by connecting the observed behavior to variables, such as vessel type, location, or features found on Nautical Charts. By determining which variables are linked to vessel behavior we can begin to develop probabilistic models to prevent collisions.

We will use COLREGS interactions to describe the interactions between ships. First, there are 3 types of encounters: overtaking, crossing, or meeting. 

Second, COLREGs apply different standards to vessels in restricted waters such as narrow channels, and traffic separation schemes, and large vessels that are restricted in their ability to maneuver. Understanding this context requires linking the AIS data to Electronic Navigational Chart data. 

Third, vessels have different hierarchies depending on the situation. Powered vessels must give way to sailing vessels, which must give way to vessels engaged in fishing, except under certain circumstances. Modeling ships behavior requires knowing the type of vessel and what it is doing during the encounter. There are several good websites for discovering vessel details including https://www.marinetraffic.com/. The ship’s activity can be inferred from AIS data (as VesselType) or observing the ships behavior.   

The USCG COLREGs Quick Reference as well as a compete COLREGs may be helpful as references.

We have a sample dataset that includes one interaction of each of the COLREGs encounters: crossing, overtaking, and meeting. The data is available on the ESRI platform and the GitHub repository. You will get extra points for using the results of challenge 1 as your inputs into challenge 2. 

The judging criteria for the challenge will include: 

Up to 30 points for model completeness and applicability. Developing techniques for filling in missing AIS data, adding variables, or predicting the behavior of vessels.

Up to 20 points for presentation and visualization
