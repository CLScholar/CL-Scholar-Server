//Query 1

db.getCollection('papers').aggregate([
  {
    $match: {    "topics": {
            $elemMatch: {
                $eq: "14"
            }
        },
        "conference": { $regex : "International Conference on Computational Linguistics", '$options': 'is' }
      }
    },
    {
      $group: {
          _id: "$year",
          num_papers: {$sum: 1}
      }
    }
])

//Query 2
// If empty record then return NO otherwise YES


//Query 3
db.getCollection('papers').aggregate([{
        $match: {
            "topics": {
                $elemMatch: {
                    $eq: "14"
                }
            },
            $or: [{
                    "conference": { $regex : "International Conference on Computational Linguistics", '$options': 'is' }
                },
                {
                    "conference": { $regex : "International Conference on Computational Linguistics", '$options': 'is' }
                }
            ]
        }
    },

    {
        $group: {
            _id: {
             "year": "$year",
             "conference": "$conference"
         },
            num_papers: {
                $sum: 1
            }
        }
    }
])

//Query 4
db.getCollection('authors').find( {"name_list": {
          $elemMatch: {
              $eq: "animesh mukherjee"
          }
      }}, {"Yearwise_Publication":1, "_id":0})

//Query 5

db.getCollection('authors').aggregate([
   {
     $lookup:
       {
         from: "papers",
         localField: "papers.paper_id",
         foreignField: "paper_id",
         as: "paperid"
       }
  },
  {
    $match: { "name_list": {
        $elemMatch: {$eq: "animesh mukherjee"}
      },
         "paperid.topics": {
            $elemMatch: {$eq: "4"}
          }
      },
  },
     {
        $unwind: '$paperid'
    },
  {
    $group: {
        _id: "$paperid.year",
        "count_paper": {$sum: 1 }
    }
   }
])

//Query 6

db.getCollection('papers').aggregate([
  {
    $match: {    "topics": {
            $elemMatch: {
                $eq: "14"
            }
        }
      }
    },
    {
      $group: {
          _id: "$year",
          num_papers: {$sum: 1}
      }
    }
])

//Query 7

db.getCollection('conferences').aggregate([
    {
    $match: {
        "name": { $regex : "International Conference on Computational Linguistics", '$options': 'is' }
      }
    },
         {
        $unwind: '$Yearwise_Publication'
    },
    {
      $group: {
          _id: "$Yearwise_Publication",
      }
    },
   {
     $replaceRoot: { newRoot: "$_id" }
   }
])

//Query 8

db.getCollection('conferences').aggregate([
    {
    $match: {
        "name": { $regex : "International Conference on Computational Linguistics", '$options': 'is' }
      }
    },
         {
        $unwind: '$Yearwise_Publication'
    },
    {
      $group: {
          _id: "$Yearwise_Publication",
      }
    },
   {
     $replaceRoot: { newRoot: "$_id" }
   }
])


//Query 9

db.getCollection('papers').aggregate([
    {
    $match: {    "topics": {
            $elemMatch: {
                $eq: "8"
            }
        }
      }
    },
    {
        $unwind: "$citation_trend"
    },
    {
        $project: {
            "sumCit" : {$sum: "$citation_trend.citation"},
            "CitTrend" : "$citation_trend",
            title: "$title"
        }
    },
    {
        $sort: {
            "sumCit": -1
        }
    },
    {
        $limit: 5
    },
    {
      $project: {
          _id: "$title",
          num_papers: "$sumCit",
          cit_trend: "$CitTrend",
      }
    }
])


//Query 10

db.getCollection('authors').aggregate([
   {
     $lookup:
       {
         from: "papers",
         localField: "papers.paper_id",
         foreignField: "paper_id",
         as: "paperid"
       }
  },
  {
    $match: { "name_list": {
        $elemMatch: {$eq: "animesh mukherjee"}
      },
         "paperid.topics": {
            $elemMatch: {$eq: "4"}
          }
      },
  },
        {
        $unwind: '$paperid'
    },
  {
    $group: {
        _id: "$paperid.year",
        "count_paper": {$sum: 1 }
    }
   },
   {
       $sort: {
           "_id": 1
       }
   }
])

**************************************
            //Query 11

db.getCollection('authors').aggregate([
            {
                $match: { 'name_list' : { $in: ['animesh mukherjee','pawan goyal'] } },
            },
            {
                "$group": {
                    "_id": 0,
                    "set1": { "$first": "$papers.paper_id" },
                    "set2": { "$last": "$papers.paper_id" }
                }
            },
            {
                "$project": { 
                    "commonToBoth": { "$setIntersection": [ "$set1", "$set2" ] }, 
                    "_id": 0 
                }
            },
            ])



**************************************

//Query 13

db.getCollection('authors').aggregate([
   {
     $lookup:
       {
         from: "papers",
         localField: "papers.paper_id",
         foreignField: "paper_id",
         as: "paperid"
       }
  },
  {
    $match: { 
         "paperid.topics": {
            $elemMatch: {$eq: "4"}
          }
      },
  },
  {$unwind: '$paperid'},
  {
    $group: {
        _id: "$author_id",
        "sumCit" : {$sum: "$paperid.citation_trend"},
        "CitTrend" : "$paperid.citation_trend"
    }
   },
   {$sort: {"sumCit": -1} },
   {limit: 1},
   {
       $project: {
           _id: "$author_id",
           "numCit": "$sumCit",
           "citTrend": "$CitTrend"
       }
   }
])
